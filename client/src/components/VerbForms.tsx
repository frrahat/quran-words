import { VerbForms as VerbFormsType } from "../types";
import "./VerbForms.scss";

function VerbForm({ verbFormName, verbFormValue }: {
  verbFormName: string,
  verbFormValue: string | undefined,
}) {
  return (
    <div className="VerbForm">
      <div className="VerbForm-name">
        {verbFormName}
      </div>
      <div className="VerbForm-value">
        {verbFormValue}
      </div>
    </div>
  )
}

function VerbForms({ verbForms }: {
  verbForms: VerbFormsType,
}) {

  const { verb_type, perfect, imperative, active_participle, passive_participle, verbal_noun } = verbForms;

  return (
    <div className="VerbForms">
      <div className="VerbForms-header">
        Verb Forms
      </div>
      <div className="VerbForms-items">
        <VerbForm verbFormName="Verb Type" verbFormValue={verb_type} />
        <VerbForm verbFormName="Perfect" verbFormValue={perfect} />
        <VerbForm verbFormName="Imperative" verbFormValue={imperative} />
        <VerbForm verbFormName="Active Participle" verbFormValue={active_participle} />
        <VerbForm verbFormName="Passive Participle" verbFormValue={passive_participle} />
        <VerbForm verbFormName="Verbal Noun" verbFormValue={verbal_noun} />
      </div>
    </div>
  )
}

export default VerbForms;
