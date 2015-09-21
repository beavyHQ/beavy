import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import { loadPMs } from '../actions';
import { PRIVATE_MESSAGES } from '../reducers';
// import CloakingList from 'components/CloakingList';

function topPosition(domElt) {
  if (!domElt) {
    return 0;
  }
  return domElt.offsetTop + topPosition(domElt.offsetParent);
}

class InfiniteScrollingList extends Component{

  getDefaultProps() {
    return {
      hasMore: false,
      loadMore() {},
      threshold: 250
    };
  }
  componentDidMount() {
    this.attachScrollListener();
  }
  componentDidUpdate() {
    this.attachScrollListener();
  }
  render() {
    var props = this.props;
    return <div ref='main'>
            {props.children}
           </div>;
  }
  scrollListener() {
    var el = React.findDOMNode(this.refs.main);
    var scrollTop = (window.pageYOffset !== undefined) ? window.pageYOffset : (document.documentElement || document.body.parentNode || document.body).scrollTop;
    if ((topPosition(el) + el.offsetHeight - scrollTop - window.innerHeight) < Number(this.props.threshold)) {
      this.detachScrollListener();
      // call loadMore after detachScrollListener to allow
      // for non-async loadMore functions
      !this.props.loading && this.props.loadMore();
    }
  }
  attachScrollListener() {
    if (!this.props.hasMore) {
      return;
    }
    window.addEventListener('scroll', ::this.scrollListener);
    window.addEventListener('resize', ::this.scrollListener);
    this.scrollListener();
  }
  detachScrollListener() {
    window.removeEventListener('scroll', ::this.scrollListener);
    window.removeEventListener('resize', ::this.scrollListener);
  }
  componentWillUnmount() {
    this.detachScrollListener();
  }
}


class SimpleListItem extends Component{

  // static propTypes = {
  //   // collection: PropTypes.object.isRequired,
  //   item: PropTypes.shape({
  //     type: PropTypes.string.isRequired,
  //     id: PropTypes.number.isRequired,
  //   })
  // }

  render(){
    return <div>{this.props.item.type}, {this.props.item.id}</div>

    const entry = this.props.collection[this.props.item.id];
    console.log("YO", entry);
    return <div>{entry.title}</div>
  }
}

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
        <InfiniteScrollingList
          hasMore={private_messages.meta.has_next}
          loadMore={::this.loadMore}
          threshold={250}
          loading={private_messages.isFetching}
          >
          {private_messages.data.map(x=>
              <SimpleListItem item={x} />
            )}
        </InfiniteScrollingList>
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