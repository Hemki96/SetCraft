export interface PlaceholderScreenProps {
  title: string;
  summary: string;
  scopeItems: ReadonlyArray<string>;
}

export function PlaceholderScreen({
  title,
  summary,
  scopeItems,
}: PlaceholderScreenProps): JSX.Element {
  return (
    <section className="screen-card" aria-label={`${title} placeholder`}>
      <header>
        <h2>{title}</h2>
        <p>{summary}</p>
      </header>

      <div>
        <h3>Geplanter Scope</h3>
        <ul>
          {scopeItems.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </div>
    </section>
  );
}
