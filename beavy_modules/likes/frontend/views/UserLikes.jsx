import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'
import { loadUserLikes } from '../actions'
import { USER_LIKES } from '../reducers'

function checkUserLikes (props) {
  const {likes, userId} = props
  if (likes) return true
  props.dispatch(loadUserLikes(userId))
}

class UserLikesView extends Component {

  static propTypes = {
    dispatch: PropTypes.func,
    userId: PropTypes.string.isRequired,
    likes: PropTypes.object
  }

  componentWillMount () {
    checkUserLikes(this.props)
  }

  componentWillReceiveProps (nextProps) {
    checkUserLikes(nextProps)
  }

  render () {
    const { likes } = this.props
    if (!likes) {
      return <h1><i>Loading likes...</i></h1>
    }
    return (
      <div>
        <h1>{likes.length} Likes</h1>
      </div>
    )
  }
}

function mapStateToProps (state, ownProps) {
  const { userId } = ownProps.params
  let likes = state[USER_LIKES]
  if (!likes) { likes = null }

  return { userId, likes }
}

export default connect(
  mapStateToProps
)(UserLikesView)
