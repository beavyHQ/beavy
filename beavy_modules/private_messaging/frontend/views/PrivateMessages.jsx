import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import { loadPMs } from '../actions';
import { PRIVATE_MESSAGES } from '../reducers';

function checkUserLikes(props){
  const {private_messages} = props;
  if (private_messages && private_messages.meta) return true;
  props.dispatch(loadPMs());
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
    if (!private_messages || private_messages.isFetching) {
      return <h1><i>Loading private messages...</i></h1>;
    }
    return (
      <div>
        <h1>{private_messages.meta.total} PMs</h1>
      </div>
    );
  }
}

function mapStateToProps(state, ownProps) {
  let private_messages = state[PRIVATE_MESSAGES];
  if (!private_messages || !private_messages.meta){ private_messages = null}

  return { private_messages };
}

export default connect(
  mapStateToProps
)(PrivateMessagesView);