import React       from 'react';
import { connect } from 'react-redux';

// We define mapDispatchToProps where we'd normally use the @connect
// decorator so the data requirements are clear upfront, but then
// export the decorated component after the main class definition so
// the component can be tested w/ and w/o being connected.
// See: http://rackt.github.io/redux/docs/recipes/WritingTests.html
const mapDispatchToProps = (state) => ({
  counter : state.counter
});
export class HomeView extends React.Component {
  static propTypes = {
    dispatch : React.PropTypes.func,
    counter  : React.PropTypes.number
  }

  constructor () {
    super();
  }

  // normally you'd import an action creator, but I don't want to create
  // a file that you're just going to delete anyways!
  _increment () {
    this.props.dispatch({ type : 'COUNTER_INCREMENT' });
  }

  render () {
    return (
      <div className='container text-center'>
        <img src="http://beavy.xyz/logos/logo.svg" alt="beavy logo" width="150" />
        <h1>Wecome to Beavy!</h1>
        <p>
        Please take a look at the <a href="https://beavyhq.gitbooks.io/beavy-documentation/content/" target="_blank">documentation</a>.
        </p>
      </div>
    );
  }
}

export default connect(mapDispatchToProps)(HomeView);
