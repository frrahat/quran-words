import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
  useParams
} from "react-router-dom";

import './App.css';
import Verse from "./components/Verse";

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" render={() =>
          <Redirect to="/verses/1/1" />
        }/>
        <Route path="/verses/:suraNum/:ayahNum" children={<Page />} />
      </Switch>
    </Router>
  );
}

function Page() {
  let { suraNum, ayahNum } = useParams();

  return (
    <div>
      <h3>suraNum: {suraNum}</h3>
      <h3>ayahNum: {ayahNum}</h3>
      <Verse suraNum={suraNum} ayahNum={ayahNum} />
    </div>
  );
}

export default App;
