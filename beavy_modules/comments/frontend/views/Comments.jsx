import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'
import { loadComments } from '../actions'
import { make_url, getStoreEntity } from 'utils'
import { Link } from 'react-router'
import { COMMENTS } from '../reducers'
// import Ago from 'react-ago-component';
import InfiniteList from 'components/InfiniteList'
import { FormattedMessage } from 'react-intl'

class SimpleListItem extends Component {

  static propTypes = {
    entry: PropTypes.shape({
      type: PropTypes.string.isRequired,
      created_at: PropTypes.string,
      title: PropTypes.string,
      id: PropTypes.number.isRequired
    })
  }

  render () {
    return <Link to={make_url.account('comments/' + this.props.entry.id)}>
          <div>
            <span>{this.props.entry.created_at}</span>
            <h2>{this.props.entry.title}</h2>
          </div>
          </Link>
  }
}

const CommentListItem = connect(
  function (state, ownProps) {
    const entry = getStoreEntity(state, ownProps.item)
    return {entry: entry}
  }
)(SimpleListItem)

function checkUserComments (props) {
  const {comments} = props
  if (comments && comments.meta) return true
  props.dispatch(loadComments())
}

class PrivateMessagesView extends Component {

  static propTypes = {
    dispatch: PropTypes.func,
    comments: PropTypes.object
  }

  componentWillMount () {
    checkUserComments(this.props)
  }

  componentWillReceiveProps (nextProps) {
    checkUserComments(nextProps)
  }

  loadMore () {
    this.props.dispatch(loadComments(this.props.comments.meta.next_num))
  }

  render () {
    const { comments } = this.props
    if (!comments || !comments.meta) {
      return <FormattedMessage tag='h1' id='loading-comments' defaultMessage='loading comments ...' />
    }
    return (
      <div>
        <FormattedMessage tag='h1' count={comments.meta.total} id='comments-with-count' defaultMessage='{count} Comments' />
        <InfiniteList
          meta={comments.meta}
          loader={::this.loadMore}
          minimalItemHeight={24}
          isFetching={comments.isFetching}
          >
          {comments.data.map(x =>
              <CommentListItem item={x} />
            )}
        </InfiniteList>
      </div>
    )
  }
}

function mapStateToProps (state, ownProps) {
  let comments = state[COMMENTS]
  if (!comments || !comments.meta) { comments = null }

  return { comments }
}

export default connect(
  mapStateToProps
)(PrivateMessagesView)
