import { Schema, arrayOf } from 'normalizr';
import { objectSchema } from 'schemas';

export const like = new Schema("Like");
export const userLike = new Schema("UserLike", { idAttribute: "object_id" });

like.define({
  object: objectSchema
});

userLike.define({
  object: objectSchema
});