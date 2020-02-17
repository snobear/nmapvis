import React from 'react';
import ReactDOM from 'react-dom';
import Home from './components/Home/Home';
import 'bootstrap/dist/css/bootstrap.css';

class App extends React.Component {
  render() {
    return (
      <div>
        <Home />
      </div>
    );
  }
}

ReactDOM.render(<App />, document.getElementById('app'));
