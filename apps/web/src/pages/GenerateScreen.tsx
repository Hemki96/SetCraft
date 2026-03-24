import { FormEvent, useState } from "react";
import {
  approveGeneratedPlan,
  createExport,
  generateSessionPlan,
  generateWeekPlan,
  GeneratedPlan,
} from "../services/api";

export function GenerateScreen(): JSX.Element {
  const [targetDistance, setTargetDistance] = useState(2000);
  const [weekDistance, setWeekDistance] = useState(7200);
  const [sessionsPerWeek, setSessionsPerWeek] = useState(4);
  const [plans, setPlans] = useState<GeneratedPlan[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [lastExport, setLastExport] = useState<string | null>(null);

  const onGenerateSession = async (event: FormEvent<HTMLFormElement>): Promise<void> => {
    event.preventDefault();
    try {
      const plan = await generateSessionPlan(targetDistance);
      setPlans((current) => [plan, ...current]);
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const onGenerateWeek = async (event: FormEvent<HTMLFormElement>): Promise<void> => {
    event.preventDefault();
    try {
      const plan = await generateWeekPlan(weekDistance, sessionsPerWeek);
      setPlans((current) => [plan, ...current]);
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const onApprovePlan = async (planId: string): Promise<void> => {
    try {
      const response = await approveGeneratedPlan(planId);
      setPlans((current) => current.map((plan) => (plan.id === planId ? response.plan : plan)));
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const onExportPlan = async (planId: string): Promise<void> => {
    try {
      const exportJob = await createExport(planId);
      setLastExport(`/api/v1/exports/${exportJob.id}/download`);
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    }
  };

  return (
    <div className="screen-stack">
      <section className="screen-card">
        <h2>Generate</h2>
        <p>Generierung, Validierung, Freigabe und Export neuer Inhalte.</p>
        {error ? <p className="error-text">{error}</p> : null}
      </section>

      <section className="screen-card">
        <h3>Session-Plan generieren</h3>
        <form className="inline-form" onSubmit={onGenerateSession}>
          <input
            type="number"
            min={200}
            value={targetDistance}
            onChange={(event) => setTargetDistance(Number(event.target.value))}
          />
          <button type="submit">Session-Plan erstellen</button>
        </form>
      </section>

      <section className="screen-card">
        <h3>Wochenplan generieren</h3>
        <form className="inline-form" onSubmit={onGenerateWeek}>
          <input
            type="number"
            min={600}
            value={weekDistance}
            onChange={(event) => setWeekDistance(Number(event.target.value))}
          />
          <input
            type="number"
            min={1}
            max={14}
            value={sessionsPerWeek}
            onChange={(event) => setSessionsPerWeek(Number(event.target.value))}
          />
          <button type="submit">Wochenplan erstellen</button>
        </form>
      </section>

      <section className="screen-card">
        <h3>Generierte Pläne</h3>
        {plans.map((plan) => (
          <article key={plan.id} className="item-card">
            <p className="mono">{plan.id.slice(0, 8)}</p>
            <p>
              Typ: {plan.plan_type} | Review: {plan.review_status} | Approval: {plan.approval_status}
            </p>
            <div className="button-row">
              <button type="button" onClick={() => void onApprovePlan(plan.id)}>
                Plan freigeben
              </button>
              <button type="button" onClick={() => void onExportPlan(plan.id)}>
                Export (JSON)
              </button>
            </div>
          </article>
        ))}
        {lastExport ? (
          <p>
            Letzter Export: <a href={lastExport}>Download</a>
          </p>
        ) : null}
      </section>
    </div>
  );
}
