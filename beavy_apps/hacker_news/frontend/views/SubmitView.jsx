import React, {Component, PropTypes} from 'react';
import { connect } from 'react-redux';
import { pushState } from 'redux-router';
import { reduxForm} from 'redux-form';
import { STORY_SUBMIT } from '../consts';
import { submitStory } from '../actions';

export class SubmitView extends React.Component {
  static propTypes = {
    fields: PropTypes.object.isRequired,
    handleSubmit: PropTypes.func.isRequired,
    isFetching: PropTypes.bool.isRequired,
    dispatch : React.PropTypes.func.isRequired
  }

  componentWillReceiveProps(nextProps){
    if (!nextProps.isFetching && nextProps.success){
      const incoming = nextProps.response[STORY_SUBMIT].data.id
      this.props.dispatch(pushState(null, '/')); //item?id=' + incoming));
    }
  }

  saveForm(formData){
    this.props.dispatch(submitStory(formData));
  }

  render () {
    const { fields: {title, url, text},
            handleSubmit, dispatch, isFetching} = this.props;
    return (
      <form name="submit_story_form" onSubmit={handleSubmit(this.saveForm.bind(this))} disabled={isFetching}>
        <fieldset>
          <label for="title">title</label>
          <input required id="title" type="text" name="title" {...title} />
          {title.error && title.touched && <div>{title.error}</div>}
          <label for="url">url</label>
          <input id="url" type="text" name="url" {...url} />
          {url.error && url.touched && <div>{url.error}</div>}
          <strong>or</strong>
          <label for="text">text</label>
          <textarea {...text} />
          {text.error && text.touched && <div>{text.error}</div>}
          <button type="submit" disabled={isFetching}>Submit</button>
        </fieldset>
        <p>
          Leave URL blank to submit a question or discussion.  If there is no url, the text (if any) will appear at the top of the thread.
        </p>
      </form>
    );
  }
}

export default connect(
  (state, ownProps) => {
    return { form: state.form,
             ...state[STORY_SUBMIT]};
  }
)(reduxForm({
  form: 'submit',
  fields: ['title', 'url', 'text'],
  validate: (data) => {
    const errors = {};
    if(!data.title || !data.title.trim()) {
      errors.title = 'You need to pass at least the title';
    }
    if(!data.url && !data.text) {
      errors.url = 'Please pass either a url or a text.';
    }
    return errors;
  }
})(SubmitView));
