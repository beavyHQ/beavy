import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import { fetchPMs } from '../actions';
import { PRIVATE_MESSAGES } from '../reducers';

function checkUserLikes(props){
  const {private_messages} = props;
  if (private_messages && private_messages.page) return true;
  props.dispatch(fetchPMs());
}

class PrivateMessagesView extends Component {

  static propTypes = {
    dispatch: PropTypes.func,
    private_messages: PropTypes.object
  }

  componentWillMount(){
    checkUserLikes(this.props);
  }

  componentWillReceiveProps(nextProps) {
    checkUserLikes(nextProps);
  }

  render() {
    const { private_messages } = this.props;
    if (!private_messages) {
      return <h1><i>Loading likes...</i></h1>;
    }
    return (
      <div>
        <h1>{private_messages.length} PMs</h1>
      </div>
    );
  }
}

function mapStateToProps(state, ownProps) {
  console.log(state);
  let private_messages = state[PRIVATE_MESSAGES];
  if (!private_messages){ private_messages = null}

  return { private_messages };
}

export default connect(
  mapStateToProps
)(PrivateMessagesView);