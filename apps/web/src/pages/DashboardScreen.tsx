import { useEffect, useState } from "react";
import { PlaceholderScreen } from "./PlaceholderScreen";
import { HealthStatus, checkApiHealth } from "../services/health";

export function DashboardScreen(): JSX.Element {
  const [healthStatus, setHealthStatus] = useState<HealthStatus | null>(null);

  useEffect(() => {
    let isMounted = true;

    void checkApiHealth().then((status) => {
      if (isMounted) {
        setHealthStatus(status);
      }
    });

    return () => {
      isMounted = false;
    };
  }, []);

  const healthText =
    healthStatus === null
      ? "API-Status wird geprueft."
      : healthStatus.state === "ok"
        ? `API erreichbar (${healthStatus.checkedAtIso}).`
        : `API aktuell nicht erreichbar (${healthStatus.checkedAtIso}).`;

  return (
    <div className="screen-stack">
      <PlaceholderScreen
        title="Dashboard"
        summary="Einstiegsansicht fuer Status, Aufgaben und offene Reviews."
        scopeItems={[
          "Systemstatus und Queue-Uebersicht",
          "Letzte Quellen, Sessions und Generierungen",
          "Schnelleinstiege in Review-Flows",
        ]}
      />

      <section className="screen-card" aria-label="Systemstatus">
        <h3>Systemstatus</h3>
        <p>{healthText}</p>
      </section>
    </div>
  );
}
