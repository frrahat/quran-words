import { MouseEventHandler, ReactElement } from "react";

import "./Filter.scss";

function Filter({
  filterLabel,
  filterValue,
  selectorComponent,
  onClearAction,
}: {
  filterLabel: string;
  filterValue: boolean | string | number | null | undefined;
  selectorComponent: ReactElement;
  onClearAction: () => void;
}) {
  const isUnset = filterValue === null || filterValue === undefined;

  const handleClickOnClear: MouseEventHandler<HTMLDivElement> = (event) => {
    event.stopPropagation();
    event.preventDefault();
    onClearAction();
  };

  return (
    <div className="Filter">
      <div className="Filter-Label">{filterLabel} : </div>
      <div className="Filter-Selector">{selectorComponent}</div>
      {!isUnset && (
        <div className="Filter-ClearButton" onClick={handleClickOnClear}>
          Clear
        </div>
      )}
    </div>
  );
}

export default Filter;
