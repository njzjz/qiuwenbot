Usage
=====

Firstly, one needs to prepare a JSON file that describes the job.

.. literalinclude:: ../examples/filter_all.json
   :language: json
   :linenos:

The detailed parameters can be found in `Input Parameters`_.
The password can be set by :envvar:`QIUWENBOT_PASSWORD` environment variable. It is
recommended using the bot password.

Then, one can submit the job using the following command:

.. code-block:: bash

   qiuwenbot submit filter_all.json

See `Command line interface`_ for more information.
