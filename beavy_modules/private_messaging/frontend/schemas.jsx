import { Schema, arrayOf } from 'normalizr';
import { userSchema } from 'schemas';

export const privateMessage = new Schema("PrivateMessage");

privateMessage.define({
  participants: arrayOf(userSchema)
});
