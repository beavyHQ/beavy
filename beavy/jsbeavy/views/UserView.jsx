import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'
import { loadUser } from 'actions/user'
import { getExtensions } from 'config/extensions'
import { USER } from 'reducers/user'

function checkUser (props) {
  const {user, userId} = props
  if (user && user.id === userId) return true
  props.dispatch(loadUser(userId))
}

class UserView extends Component {

  componentWillMount () {
    checkUser(this.props)
  }

  componentWillReceiveProps (nextProps) {
    checkUser(nextProps)
  }

  render () {
    const { user, userId, children } = this.props
    if (!user) {
      return <h1><i>Loading profile...</i></h1>
    }
    return (
      <div>
        <h1>{user.name} (user.id)</h1>
        <h2>Menu</h2>
        {getExtensions('userMenu').map(x => x.call(this))}

        {children}
      </div>
    )
  }
}

UserView.propTypes = {
  dispatch: PropTypes.func,
  userId: PropTypes.string.isRequired,
  user: PropTypes.object,
  checkUser: PropTypes.func.isRequired,
}

function mapStateToProps (state, ownProps) {
  const { userId } = ownProps.params
  let user = state[USER]
  if (!user || user.id !== userId) { user = null }

  return { userId, user }
}

export default connect(
  mapStateToProps
)(UserView)
