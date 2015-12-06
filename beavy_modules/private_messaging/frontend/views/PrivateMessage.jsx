import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'
import { getStoreEntity } from 'utils'
import LoadEditor from 'components/Editor'
import map from 'lodash/collection/map'

class WriteReply extends React.Component {
  constructor (props) {
    super()
    this.state = {
      editing: false,
      editor: null
    }
    this.options = {
      docFormat: 'html',
      menuBar: false,
      inlineMenu: true,
      buttonMenu: true
    }
    LoadEditor.then(x => this.setState({editor: x}))
  }

  render () {
    if (this.state.editing) {
      if (!this.state.editor) {
        return <div>Loading</div>
      }
      const Editor = this.state.editor
      return <div>
              <h3>Reply</h3>
              <Editor value={''} options={this.options} ref='editor'/>
              <button onClick={this.send.bind(this)}>Send</button>
            </div>
    }
    return <div>
             <h3>Reply</h3>
             <div onClick={x => this.setState({editing: true})}>click here to write reply</div>
           </div>
  }
  send () {
    alert(this.refs.editor.pm.getContent('markdown'))
  }
}

class PrivateMessageView extends Component {

  static propTypes = {
    dispatch: PropTypes.func,
    message: PropTypes.object.isRequired,
    participants: PropTypes.array.isRequired
  }

  render () {
    const { message, participants } = this.props

    return <div>
            <span>{message.created_at}</span>
            <h2>{message.title}</h2>
            <span>Users: {map(participants, (x) => x.name || x.id)}</span>
            <WriteReply />
          </div>
  }
}

function mapStateToProps (state, ownProps) {
  const { messageId } = ownProps.params
  const message = getStoreEntity(state, {id: messageId, type: 'private_message'})
  const participants = map(message.participants.data, x => getStoreEntity(state, x))

  return { message, participants }
}

export default connect(
  mapStateToProps
)(PrivateMessageView)
