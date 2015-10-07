import React, {Component, PropTypes} from 'react';
import { connect } from 'react-redux';
import {connectReduxForm} from 'redux-form';

export class SubmitView extends React.Component {
  static propTypes = {
    fields: PropTypes.object.isRequired,
    handleSubmit: PropTypes.func.isRequired,
    dispatch : React.PropTypes.func
  }

  saveForm(formData){
    console.log(formData);
  }

  render () {
    const { fields: {title, url, text},
            handleSubmit, dispatch } = this.props;
    return (
      <form onSubmit={handleSubmit(this.saveForm)}>
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
          <button type="submit">Submit</button>
        </fieldset>
        <p>
          Leave URL blank to submit a question or discussion.  If there is no url, the text (if any) will appear at the top of the thread.
        </p>
      </form>
    );
  }
}



// apply connectReduxForm() and include synchronous validation
export default connectReduxForm({
  form: 'submit',                      // the name of your form and the key to
                                        // where your form's state will be mounted
  fields: ['title', 'url', 'text'], // a list of all your fields in your form
  validate: (data) => {
  const errors = {};
    if(!data.title || !data.title.trim()) {
      errors.title = 'You need to pass at least the title';
    }
    if(!data.url && !data.text) {
      errors.url = 'Please pass either a url or a text.';
    }
    console.log(errors);
    return errors;
  }
})(SubmitView);

