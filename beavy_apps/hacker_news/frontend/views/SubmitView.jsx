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
export class SubmitView extends React.Component {
  static propTypes = {
    dispatch : React.PropTypes.func
  }

  constructor () {
    super();
  }

  render () {
    return (
      <div className='container text-center'>
        <label for="title">title</label>
        <input id="title" name="title" />
        <label for="url">url</label>
        <input id="url" name="url" />
        <strong>or</strong>
        <label for="text">text</label>
        <textarea />
        <button type="submit">Submit</button>
        <p>
          Leave URL blank to submit a question or discussion.  If there is no url, the text (if any) will appear at the top of the thread.
        </p>
      </div>
    );
  }
}

export default connect(mapDispatchToProps)(SubmitView);
