import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import { loadPMs } from '../actions';
import { PRIVATE_MESSAGES } from '../reducers';
import map from 'lodash/collection/map';
import InfiniteList from 'components/InfiniteList';


class SimpleListItem extends Component{

  // static propTypes = {
  //   // collection: PropTypes.object.isRequired,
  //   item: PropTypes.shape({
  //     type: PropTypes.string.isRequired,
  //     id: PropTypes.number.isRequired,
  //   })
  // }

  render(){
    // return <div>{this.props.item.type}, {this.props.item.id}</div>

    // const entry = this.props.collection[this.props.item.id];
    return <div>{this.props.entry.title}</div>
  }
}

function getEntity(state, item){
  return state.entities[item.type][item.id];
}

const PMListItem = connect(
  function(state, ownProps){
    const entry = getEntity(state, ownProps.item),
          participants = map(entry.participants.data, x=> getEntity(state, x));
    return {entry: entry, participants: participants}
  }
)(SimpleListItem)

function checkUserPMs(props){
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
    checkUserPMs(this.props);
  }

  componentWillReceiveProps(nextProps) {
    checkUserPMs(nextProps);
  }

  loadMore(){
    this.props.dispatch(loadPMs(this.props.private_messages.meta.next_num));
  }

  render() {
    const { private_messages } = this.props;
    if (!private_messages || !private_messages.meta) {
      return <h1><i>Loading private messages...</i></h1>;
    }
    return (
      <div>
        <h1>{private_messages.meta.total} PMs</h1>
        <InfiniteList
          meta={private_messages.meta}
          loader={::this.loadMore}
          minimalItemHeight={24}
          isFetching={private_messages.isFetching}
          >
          {private_messages.data.map(x=>
              <PMListItem item={x} />
            )}
        </InfiniteList>
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