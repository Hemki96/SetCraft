import { PlaceholderScreen } from "./PlaceholderScreen";

export function ExportScreen(): JSX.Element {
  return (
    <PlaceholderScreen
      title="Exports"
      summary="Export v1 fuer freigegebene Inhalte in nutzbare Formate."
      scopeItems={[
        "Nur Inhalte mit Freigabestatus 'approved' exportieren",
        "Exportformate: JSON und TXT",
        "Download-Flow mit auditierbarer Protokollierung",
      ]}
    />
  );
}
