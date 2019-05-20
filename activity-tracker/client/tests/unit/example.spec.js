import Activities from '@/components/Activities.vue';
import { mount } from '@vue/test-utils';
// mount creates wrapper that contains the mounted (mocked) component
// var assert = require('assert');
var expect = require('chai').expect;

describe('Activities.vue', () => {
  it('mounts component', () => {
    const wrapper = mount(Activities);
    expect(wrapper.isVueInstance()).to.be.true;
  });

  it('calls api to get all activities', () => {
    expect(typeof Activities.data).to.exist;
  });
});
