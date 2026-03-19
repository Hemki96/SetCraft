import { Navigate, createBrowserRouter } from "react-router-dom";
import { AppShell } from "../layout/AppShell";
import { DashboardScreen } from "../pages/DashboardScreen";
import { GenerateScreen } from "../pages/GenerateScreen";
import { LoginScreen } from "../pages/LoginScreen";
import { SessionsScreen } from "../pages/SessionsScreen";
import { SourcesScreen } from "../pages/SourcesScreen";

export const appRouter = createBrowserRouter([
  {
    path: "/",
    element: <AppShell />,
    children: [
      { index: true, element: <Navigate to="/dashboard" replace /> },
      { path: "login", element: <LoginScreen /> },
      { path: "dashboard", element: <DashboardScreen /> },
      { path: "sources", element: <SourcesScreen /> },
      { path: "sessions", element: <SessionsScreen /> },
      { path: "generate", element: <GenerateScreen /> },
      { path: "*", element: <Navigate to="/dashboard" replace /> },
    ],
  },
]);
