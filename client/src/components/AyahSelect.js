import { suraList } from "../config";
import NumberSelect from "./NumberSelect";

import "./AyahSelect.css";

function AyahSelect({
  valueClassName,
  selectedSuraNum,
  selectedAyahNum,
  onSelectAyah,
}) {
  const ayahCount = suraList[selectedSuraNum - 1]?.ayah_count || 0;

  return (
    <NumberSelect
      valueClassName={valueClassName}
      selectedNumber={selectedAyahNum}
      startNumber={1}
      endNumber={ayahCount}
      onSelectNumber={(number) => onSelectAyah(number)}
    />
  );
}

export default AyahSelect;
