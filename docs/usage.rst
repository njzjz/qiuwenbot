Usage
=====

Firstly, one needs to prepare a JSON file that describes the job.

.. literalinclude:: ../examples/filter_all.json
   :language: json
   :linenos:

The detailed parameters can be found in :ref:`Input Parameters <args>`.
The password can be set by :envvar:`QIUWENBOT_PASSWORD` environment variable. It is
recommended using the bot password.

Then, one can submit the job using the following command:

.. code-block:: bash

   qiuwenbot submit filter_all.json

See :ref:`Command line interface <cli>` for more information.
