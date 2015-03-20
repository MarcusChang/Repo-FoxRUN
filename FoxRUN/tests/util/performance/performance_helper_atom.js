'use strict';

(function(window) {

  var perfMeasurements;

  window.PerformanceHelperAtom = {
    getMeasurements: function(event) {
      console.log('event',event);
      perfMeasurements[event]  = window.performance.now();
      return  perfMeasurements
    },

    init: function() {

      perfMeasurements = Object.create(null);
      perfMeasurements.start = window.performance.now();

    },
    unregister: function() {
          // note: we're not reseting mozPerfHasListener to false here because at
          // this point we basically don't mind if the app keeps sending perf
          // events.

          marionetteScriptFinished();
      }

  };

  window.PerformanceHelperAtom.init();
})(window.wrappedJSObject);

