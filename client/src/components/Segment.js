import './Segment.css';

function Segment({ segment }) {
  const { arabic, pos_full, pos_color } = segment;

  return (
    <div className="Segment" style={{color: pos_color}}>
      <div className="Segment-arabic">{arabic}</div>
      <div className="Segment-pos">{pos_full}</div>
    </div>
  )
}

export default Segment;
