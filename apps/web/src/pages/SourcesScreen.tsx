import { PlaceholderScreen } from "./PlaceholderScreen";

export function SourcesScreen(): JSX.Element {
  return (
    <PlaceholderScreen
      title="Sources"
      summary="Bereich fuer Upload, Uebersicht und Detailansicht historischer Quellen."
      scopeItems={[
        "Source Upload Screen",
        "Source List Screen",
        "Source Detail Screen",
      ]}
    />
  );
}
