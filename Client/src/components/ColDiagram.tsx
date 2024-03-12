export const ColDiagram = ({ data }: { data: number[] }) => {
  return (
    <div>
      {data.map((x) => {
        return <div style={`height: ${x};`}></div>;
      })}
    </div>
  );
};
