import { NavLink, Outlet } from "react-router-dom";

const PRIMARY_NAV_ITEMS = [
  { to: "/login", label: "Login" },
  { to: "/dashboard", label: "Dashboard" },
  { to: "/sources", label: "Sources" },
  { to: "/sessions", label: "Sessions" },
  { to: "/approvals", label: "Approvals" },
  { to: "/generate", label: "Generate" },
  { to: "/exports", label: "Exports" },
] as const;

const STATUS_HINTS = [
  "Historisch",
  "Generiert",
  "Geprueft",
  "Freigegeben",
  "Warnung",
] as const;

export function AppShell(): JSX.Element {
  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="brand-block">
          <h1>SetCraft</h1>
          <p>Training Plan Platform</p>
        </div>
        <div className="status-hints" aria-label="Statuslegende">
          {STATUS_HINTS.map((hint) => (
            <span key={hint} className="status-chip">
              {hint}
            </span>
          ))}
        </div>
      </header>

      <nav className="main-nav" aria-label="Primary navigation">
        {PRIMARY_NAV_ITEMS.map((item) => (
          <NavLink
            key={item.to}
            className={({ isActive }) =>
              isActive ? "nav-link nav-link-active" : "nav-link"
            }
            to={item.to}
          >
            {item.label}
          </NavLink>
        ))}
      </nav>

      <main className="content-shell">
        <Outlet />
      </main>
    </div>
  );
}
