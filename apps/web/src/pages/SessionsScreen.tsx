import { PlaceholderScreen } from "./PlaceholderScreen";

export function SessionsScreen(): JSX.Element {
  return (
    <PlaceholderScreen
      title="Sessions"
      summary="Bereich fuer Suche, Detailansicht und Review von Trainingseinheiten."
      scopeItems={[
        "Session Search Screen",
        "Session Detail / Review Screen",
      ]}
    />
  );
}
