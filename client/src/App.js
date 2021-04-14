import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
  useParams
} from "react-router-dom";

import './App.css';

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" render={() =>
          <Redirect to="/verses/1/1" />
        }/>
        <Route path="/verses/:suraNum/:ayahNum" children={<Child />} />
      </Switch>
    </Router>
  );
}

function Child() {
  let { suraNum, ayahNum } = useParams();

  return (
    <div>
      <h3>suraNum: {suraNum}</h3>
      <h3>ayahNum: {ayahNum}</h3>
    </div>
  );
}

export default App;
