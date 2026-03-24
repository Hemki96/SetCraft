import { PlaceholderScreen } from "./PlaceholderScreen";

export function ApprovalScreen(): JSX.Element {
  return (
    <PlaceholderScreen
      title="Approvals"
      summary="Freigabeflow fuer Sessions und generierte Plaene mit rollenbasierter Berechtigung (Admin/Trainer)."
      scopeItems={[
        "Freigabe-Queue fuer pending Inhalte",
        "Rollenhinweis: Nur Admin darf final freigeben",
        "Audit-Hinweise fuer jede kritische Aktion",
      ]}
    />
  );
}
