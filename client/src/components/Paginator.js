import { Link } from "react-router-dom";

import './Paginator.css';

function PaginatorButton({ link, text, isDisabled }) {
  return (
    <button
      className="Paginator-btn"
      disabled={isDisabled}
    >
      {
        isDisabled ? text : <Link to={link}>{text}</Link>
      }
    </button>
  )
}

function Paginator({ currentPage, max, getPageLink }) {
  return (
    <div className="Paginator">
      <PaginatorButton
        link={getPageLink(currentPage - 1)}
        text='Prev'
        isDisabled={currentPage <= 1}
      />
      <PaginatorButton
        link={getPageLink(currentPage + 1)}
        text='Next'
        isDisabled={currentPage >= max}
      />
    </div>
  )
}

export default Paginator;
