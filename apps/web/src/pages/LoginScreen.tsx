import { PlaceholderScreen } from "./PlaceholderScreen";

export function LoginScreen(): JSX.Element {
  return (
    <PlaceholderScreen
      title="Login"
      summary="Authentifizierungseinstieg als Platzhalter ohne aktive Session-Logik."
      scopeItems={[
        "Anmeldeformular (MVP)",
        "Rollenbasierte Weiterleitung",
        "Session-Status und Fehlermeldungen",
      ]}
    />
  );
}
