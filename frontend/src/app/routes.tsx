// frontend/src/router.tsx
import { createBrowserRouter, Navigate } from "react-router-dom";
import { useAuth } from "./context/AuthContext";
import { LandingPage } from "./pages/LandingPage";
import { LoginPage } from "./pages/LoginPage";
import { RegisterPage } from "./pages/RegisterPage";
import { DashboardPage } from "./pages/DashboardPage";
import { QuizPage } from "./pages/QuizPage";
import { ResultsPage } from "./pages/ResultsPage";
import { AdminDashboard } from "./pages/AdminDashboard";
import { TeacherDashboard } from "./pages/TeacherDashboard";
import { MediaPage } from "./pages/MediaPage";
import { SuperAdminPage } from "./pages/SuperAdminPage";
import { ProtectedRoute } from "./components/ProtectedRoute";

export const router = createBrowserRouter([
  { path: "/", Component: LandingPage },
  { path: "/login", Component: LoginPage },
  { path: "/register", Component: RegisterPage },
  { path: "/dashboard", Component: DashboardPage },
  { path: "/quiz", Component: QuizPage },
  { path: "/results", Component: ResultsPage },
  { path: "/admin", Component: AdminDashboard },
  { path: "/teacher", Component: TeacherDashboard },
  { path: "/media", Component: MediaPage },
  {
    path: "/superadmin",
    element: (
      <ProtectedRoute allowedRoles={["superadmin"]}> 
        <SuperAdminPage />
      </ProtectedRoute>
    ),
},
]);