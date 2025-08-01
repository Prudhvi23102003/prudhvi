// App.js
import { Routes, Route, BrowserRouter, useLocation } from "react-router-dom";
import SignIn from './SignIn/SignIn';
import StandardConfigForm from './StandardConfig/StandardConfigForm';
import UserOnboarding from "./UserOnboarding/userOnboarding";
import Header from "./Header/Header";
import Footer from "./Footer/Footer";
import Dashboard from "./Dashboard/Dashboard";
import { useEffect } from "react";

// Move this part inside a separate component so we can use hooks
function AppContent() {
  const location = useLocation();
  const isSignInPage = location.pathname === "/" || location.pathname === "/signin";

  useEffect(() => {
    window.scrollTo(0, 0); // optional: scroll to top on route change
  }, [location]);

  return (
    <>
      {!isSignInPage && <Header />}
      <main style={{ minHeight: '80vh', padding: '20px' }}>
        <Routes>
          <Route path="/" element={<SignIn />} />
          <Route path="/signin" element={<SignIn />} />
          <Route path="/config" element={<StandardConfigForm />} />
          <Route path="/UserOnboarding" element={<UserOnboarding />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </main>
      {!isSignInPage && <Footer />}
    </>
  );
}
function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

export default App;


