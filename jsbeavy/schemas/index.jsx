import { Schema } from 'normalizr';
import { getNamedExtensions } from 'config/extensions';

export const objectSchema = new Schema('Object');
export const userSchema = new Schema('User');
export const activitySchema = new Schema('Activity');

export function setupSchemas(){
  objectSchema.define(getNamedExtensions("objectSchema"));
  userSchema.define(getNamedExtensions("userSchema"));
  activitySchema.define(getNamedExtensions("activitySchemas"));
}