import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import ItemList from './containers/itemList.js';

// var reducer = require("./reducer.jsx");
// var store = redux.createStore(reducer);
//
// store.dispatch({
//   type: "SET_STATE",
//   state: {
//     phones: [ "iPhone 7 Plus", "Samsung Galaxy A5" ]
//   }
// });


class App extends Component {

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <p className="App-intro">
          <ItemList/>
        </p>
      </div>
    );
  }
}




export default App;
