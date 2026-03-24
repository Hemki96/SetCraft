import { PlaceholderScreen } from "./PlaceholderScreen";

export function LoginScreen(): JSX.Element {
  return (
    <PlaceholderScreen
      title="Login"
      summary="Authentifizierungseinstieg mit Rollenmodell v1 (Admin/Trainer)."
      scopeItems={[
        "Anmeldeformular (MVP)",
        "Rollenbasierte Weiterleitung (admin/trainer)",
        "Session-Status und Fehlermeldungen",
      ]}
    />
  );
}
