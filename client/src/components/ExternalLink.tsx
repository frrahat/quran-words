import "./ExternalLink.scss";

const ExternalLink = ({ link, text }: { link: string, text: string }) => (
  <a
    key={text}
    className="ExternalLink"
    href={link}
    target="_blank"
    rel="noreferrer">
    {text}
  </a>
);

export default ExternalLink;
