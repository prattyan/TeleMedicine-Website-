#!/usr/bin/env node
// Database backup and data integrity verification script
// Run this script periodically to ensure data permanence

const mysql = require('mysql2/promise');
const fs = require('fs').promises;
const path = require('path');

// Database configuration
const DB_CONFIG = {
  host: process.env.DB_HOST || 'localhost',
  port: process.env.DB_PORT || 3306,
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || '',
  database: process.env.DB_NAME || 'telemedicine'
};

class DatabaseBackupManager {
  constructor() {
    this.backupDir = path.join(__dirname, '../backups');
    this.logFile = path.join(__dirname, '../logs/backup.log');
  }

  async initialize() {
    // Create backup and log directories if they don't exist
    try {
      await fs.mkdir(this.backupDir, { recursive: true });
      await fs.mkdir(path.dirname(this.logFile), { recursive: true });
    } catch (error) {
      console.error('Failed to create directories:', error);
    }
  }

  async log(message) {
    const timestamp = new Date().toISOString();
    const logEntry = `[${timestamp}] ${message}\n`;
    console.log(logEntry.trim());
    
    try {
      await fs.appendFile(this.logFile, logEntry);
    } catch (error) {
      console.error('Failed to write to log file:', error);
    }
  }

  async createBackup() {
    const connection = await mysql.createConnection(DB_CONFIG);
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupFile = path.join(this.backupDir, `backup-${timestamp}.sql`);

    try {
      await this.log('Starting database backup...');

      // Get list of all tables
      const [tables] = await connection.execute('SHOW TABLES');
      let backupContent = `-- TeleMedicine Database Backup\n-- Created: ${new Date().toISOString()}\n-- Database: ${DB_CONFIG.database}\n\n`;

      backupContent += `SET FOREIGN_KEY_CHECKS = 0;\n\n`;

      for (const table of tables) {
        const tableName = Object.values(table)[0];
        await this.log(`Backing up table: ${tableName}`);

        // Get table structure
        const [createTable] = await connection.execute(`SHOW CREATE TABLE \`${tableName}\``);
        backupContent += `-- Table structure for ${tableName}\n`;
        backupContent += `DROP TABLE IF EXISTS \`${tableName}\`;\n`;
        backupContent += createTable[0]['Create Table'] + ';\n\n';

        // Get table data
        const [rows] = await connection.execute(`SELECT * FROM \`${tableName}\``);
        
        if (rows.length > 0) {
          backupContent += `-- Data for table ${tableName}\n`;
          backupContent += `LOCK TABLES \`${tableName}\` WRITE;\n`;
          
          const columns = Object.keys(rows[0]);
          const columnList = columns.map(col => `\`${col}\``).join(', ');
          
          for (const row of rows) {
            const values = columns.map(col => {
              const value = row[col];
              if (value === null) return 'NULL';
              if (typeof value === 'string') return `'${value.replace(/'/g, "''")}'`;
              if (value instanceof Date) return `'${value.toISOString().slice(0, 19).replace('T', ' ')}'`;
              return value;
            }).join(', ');
            
            backupContent += `INSERT INTO \`${tableName}\` (${columnList}) VALUES (${values});\n`;
          }
          
          backupContent += `UNLOCK TABLES;\n\n`;
        }
      }

      backupContent += `SET FOREIGN_KEY_CHECKS = 1;\n`;

      // Write backup file
      await fs.writeFile(backupFile, backupContent);
      await this.log(`Backup completed successfully: ${backupFile}`);

      // Verify backup file
      const stats = await fs.stat(backupFile);
      await this.log(`Backup file size: ${(stats.size / 1024 / 1024).toFixed(2)} MB`);

      return backupFile;

    } catch (error) {
      await this.log(`Backup failed: ${error.message}`);
      throw error;
    } finally {
      await connection.end();
    }
  }

  async verifyDataIntegrity() {
    const connection = await mysql.createConnection(DB_CONFIG);

    try {
      await this.log('Starting data integrity verification...');

      // Check for orphaned records
      const orphanedQueries = [
        {
          name: 'Orphaned Patients',
          query: 'SELECT COUNT(*) as count FROM patients p LEFT JOIN users u ON p.user_id = u.id WHERE u.id IS NULL'
        },
        {
          name: 'Orphaned Doctors',
          query: 'SELECT COUNT(*) as count FROM doctors d LEFT JOIN users u ON d.user_id = u.id WHERE u.id IS NULL'
        },
        {
          name: 'Orphaned Health Workers',
          query: 'SELECT COUNT(*) as count FROM healthworkers h LEFT JOIN users u ON h.user_id = u.id WHERE u.id IS NULL'
        }
      ];

      let integrityIssues = 0;

      for (const check of orphanedQueries) {
        const [result] = await connection.execute(check.query);
        const count = result[0].count;
        
        if (count > 0) {
          await this.log(`⚠️  ${check.name}: ${count} orphaned records found`);
          integrityIssues++;
        } else {
          await this.log(`✅ ${check.name}: No issues found`);
        }
      }

      // Check data consistency
      const consistencyChecks = [
        {
          name: 'Users with missing profiles',
          query: `SELECT u.id, u.role FROM users u 
                  LEFT JOIN patients p ON u.id = p.user_id AND u.role = 'patient'
                  LEFT JOIN doctors d ON u.id = d.user_id AND u.role = 'doctor'  
                  LEFT JOIN healthworkers h ON u.id = h.user_id AND u.role = 'healthworker'
                  WHERE p.user_id IS NULL AND d.user_id IS NULL AND h.user_id IS NULL`
        }
      ];

      for (const check of consistencyChecks) {
        const [result] = await connection.execute(check.query);
        
        if (result.length > 0) {
          await this.log(`⚠️  ${check.name}: ${result.length} issues found`);
          integrityIssues++;
        } else {
          await this.log(`✅ ${check.name}: No issues found`);
        }
      }

      // Generate statistics
      const [userStats] = await connection.execute(`
        SELECT 
          role,
          COUNT(*) as count,
          COUNT(CASE WHEN is_active = 1 THEN 1 END) as active_count
        FROM users 
        GROUP BY role
      `);

      await this.log('📊 Current user statistics:');
      for (const stat of userStats) {
        await this.log(`   ${stat.role}: ${stat.count} total, ${stat.active_count} active`);
      }

      if (integrityIssues === 0) {
        await this.log('✅ Data integrity verification completed successfully - No issues found');
      } else {
        await this.log(`⚠️  Data integrity verification completed with ${integrityIssues} issues`);
      }

      return integrityIssues === 0;

    } catch (error) {
      await this.log(`Data integrity verification failed: ${error.message}`);
      throw error;
    } finally {
      await connection.end();
    }
  }

  async cleanupOldBackups(daysToKeep = 30) {
    try {
      const files = await fs.readdir(this.backupDir);
      const backupFiles = files.filter(file => file.startsWith('backup-') && file.endsWith('.sql'));
      
      const cutoffDate = new Date();
      cutoffDate.setDate(cutoffDate.getDate() - daysToKeep);

      let deletedCount = 0;

      for (const file of backupFiles) {
        const filePath = path.join(this.backupDir, file);
        const stats = await fs.stat(filePath);
        
        if (stats.mtime < cutoffDate) {
          await fs.unlink(filePath);
          deletedCount++;
          await this.log(`Deleted old backup: ${file}`);
        }
      }

      await this.log(`Cleanup completed: ${deletedCount} old backups removed`);
      
    } catch (error) {
      await this.log(`Backup cleanup failed: ${error.message}`);
    }
  }

  async generateHealthReport() {
    const connection = await mysql.createConnection(DB_CONFIG);

    try {
      await this.log('Generating database health report...');

      // Database size information
      const [sizeInfo] = await connection.execute(`
        SELECT 
          table_name,
          ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb
        FROM information_schema.tables 
        WHERE table_schema = ?
        ORDER BY (data_length + index_length) DESC
      `, [DB_CONFIG.database]);

      await this.log('📊 Database table sizes:');
      for (const table of sizeInfo) {
        await this.log(`   ${table.table_name}: ${table.size_mb} MB`);
      }

      // Recent activity
      const [recentUsers] = await connection.execute(`
        SELECT 
          COUNT(*) as count,
          DATE(created_at) as date
        FROM users 
        WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAYS)
        GROUP BY DATE(created_at)
        ORDER BY date DESC
      `);

      await this.log('📈 New registrations in last 7 days:');
      for (const day of recentUsers) {
        await this.log(`   ${day.date}: ${day.count} new users`);
      }

    } catch (error) {
      await this.log(`Health report generation failed: ${error.message}`);
    } finally {
      await connection.end();
    }
  }
}

// Main execution
async function main() {
  const backupManager = new DatabaseBackupManager();
  await backupManager.initialize();

  try {
    // Create backup
    await backupManager.createBackup();
    
    // Verify data integrity
    await backupManager.verifyDataIntegrity();
    
    // Generate health report
    await backupManager.generateHealthReport();
    
    // Cleanup old backups
    await backupManager.cleanupOldBackups(30);
    
    await backupManager.log('🎉 All database maintenance tasks completed successfully');
    
  } catch (error) {
    await backupManager.log(`❌ Database maintenance failed: ${error.message}`);
    process.exit(1);
  }
}

// Run if this file is executed directly
if (require.main === module) {
  main().catch(console.error);
}

module.exports = { DatabaseBackupManager };