import { PlaceholderScreen } from "./PlaceholderScreen";

export function GenerateScreen(): JSX.Element {
  return (
    <PlaceholderScreen
      title="Generate"
      summary="Bereich fuer die statusorientierte Vorbereitung neuer Vorschlaege."
      scopeItems={[
        "Generation Form – Session",
        "Generation Form – Week Plan",
        "Generated Plan Detail Screen",
        "Export Screen / Export State",
      ]}
    />
  );
}
