import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'
import { getStoreEntity } from 'utils'

class LinkView extends Component {

  static propTypes = {
    dispatch: PropTypes.func,
    link: PropTypes.object.isRequired
  }

  render () {
    const { link } = this.props

    return <div>
            <span>{link.created_at}</span>
            <h2><a href={link.url} target='_blank'>{link.title}</a></h2>
          </div>
  }
}

function mapStateToProps (state, ownProps) {
  const { linkId } = ownProps.params
  const link = getStoreEntity(state, {id: linkId, type: 'link'})

  return { link }
}

export default connect(
  mapStateToProps
)(LinkView)
