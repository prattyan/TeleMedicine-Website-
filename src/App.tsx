import { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from "react-router-dom";
import { LanguageProvider } from "./context/LanguageContext";
import { AuthProvider, useAuth } from "./auth/AuthContext"; // ✅ NEW
import Header from "./component/Header";
import Hero from "./component/Hero";
import ProblemStatement from "./component/ProblemStatement";
import Solution from "./component/Solution";
import ServiceAreaMap from "./component/ServiceAreaMap";
import Footer from "./component/Footer";
import SignIn from "./component/SignIn";
import Registration from "./component/Registration";
import PatientLanding from "./component/PatientLanding";
import DoctorLanding from "./component/DoctorLanding";
import HealthworkerLanding from "./component/HealthworkerLanding";
import DatabaseAdmin from "./component/DatabaseAdmin";
import ImpactSection from "./component/ImpactSection";
//dhur bara baler ekta comment
// ✅ Wrapper to use Header + Homepage
function HomeLayout() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const navigate = useNavigate();

  return (
    <>
      <Header
        mobileMenuOpen={mobileMenuOpen}
        setMobileMenuOpen={setMobileMenuOpen}
        onSignInClick={() => navigate("/signin")}
      />
      <Hero />
      <ProblemStatement />
      <Solution />
      <ServiceAreaMap />
      <ImpactSection />
      <Footer />
    </>
  );
}

// ✅ ProtectedRoute wrapper to restrict access to signed-in users
function ProtectedRoute({ children, allowedRole }: { children: JSX.Element; allowedRole?: string }) {
  const { token, user } = useAuth();

  if (!token) {
    // If not logged in → redirect to signin
    return <Navigate to="/signin" replace />;
  }

  if (allowedRole && user?.role !== allowedRole) {
    // If user doesn't have permission → redirect home
    return <Navigate to="/" replace />;
  }

  return children;
}

function App() {
  return (
    <LanguageProvider>
      <AuthProvider>
        <Router>
          <div className="min-h-screen bg-white">
            <Routes>
              {/* Public Pages */}
              <Route path="/" element={<HomeLayout />} />
              <Route path="/signin" element={<SignIn />} />
              <Route path="/register" element={<Registration />} />
              <Route path="/admin" element={<DatabaseAdmin />} />

              {/* ✅ Protected Dashboard Routes */}
              <Route
                path="/patient-landing"
                element={
                  <ProtectedRoute allowedRole="patient">
                    <PatientLanding />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/doctor-landing"
                element={
                  <ProtectedRoute allowedRole="doctor">
                    <DoctorLanding />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/healthworker-landing"
                element={
                  <ProtectedRoute allowedRole="healthworker">
                    <HealthworkerLanding />
                  </ProtectedRoute>
                }
              />
            </Routes>
          </div>
        </Router>
      </AuthProvider>
    </LanguageProvider>
  );
}

export default App;
