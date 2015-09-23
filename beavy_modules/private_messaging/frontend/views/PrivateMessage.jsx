import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import { loadPMs } from '../actions';
import { make_url, getStoreEntity } from 'utils';
import { Link } from 'react-router';
import { PRIVATE_MESSAGES } from '../reducers';
import Ago from 'react-ago-component';
import map from 'lodash/collection/map';
import InfiniteList from 'components/InfiniteList';


class PrivateMessageView extends Component {

  static propTypes = {
    dispatch: PropTypes.func,
    message: PropTypes.object.isRequired,
    participants: PropTypes.array.isRequired,
  }

  render() {
    const { message, participants } = this.props;

    return <div>
            <Ago date={message.created_at} />
            <h2>{message.title}</h2>
            <span>Users: {map(participants, (x) => x.name || x.id)}</span>
          </div>;
  }
}

function mapStateToProps(state, ownProps) {
  const { messageId } = ownProps.params,
        message = getStoreEntity(state , {id: messageId, type: "private_message"}),
        participants = map(message.participants.data, x => getStoreEntity(state, x))

  return { message, participants };
}

export default connect(
  mapStateToProps
)(PrivateMessageView);