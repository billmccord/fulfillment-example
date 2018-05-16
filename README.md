# Simple Store to Warehouse Order Sync

## Overview

This simple project illustrates a Django fulfillment application that allows synchronizing orders between a store and a warehouse.

This implementation is not robust and makes the following assumptions:

- Order monetary information is not shared with the warehouse. This was primarily to illustrate that the models could be different, but should still be sync-able.

- Orders will only be created using the admin tool on the store. In fact, creating orders from the warehouse via the admin tool has been disabled. This is because I don't think it makes sense for orders to originate from the warehouse.

- Orders will only be created and updated via the admin tool.

- The REST API will only be used for synchronization and will not be used by other processes to create or update orders.

- Orders will never be deleted. I didn't prevent this, but it currently doesn't sync deletes.

This implementation could easily be extended to support creates and updates via the API for reasons other than synchronization, but I didn't have time. Basically, we would just need to override the relevant methods in the OrderViewSet so that we could handle situations where creates and updates occur in a similar fashion. If this was done, it would probably be a good idea to DRY-up the code used for synchronization in the respective apps so it could be reused for this purpose.  

Similarly, we could easily support synchronizing deletes, but I'm not sure it makes sense to delete orders. Most likely we would just want to set the status to 'voided' in order to preserve the information.

## Setup

Install Postgres and setup a user

Create three databases that the user you created has full access to called:

- fulfillment
- fulfillment_store
- fulfillment_warehouse

Set environment variables if you need to override the default database host, user, and password with:

- DB_HOST (default: 'localhost')
- DB_USER (default: 'bill')
- DB_PASS (default: '')

## Further Considerations

This implementation deals with two-way synchronization primarily through the use of UUIDs in order to avoid collisions that would likely occur if we used sequential integer IDs. Even if we allowed creation to occur in the warehouse, we could still be confident that no collisions would occur given the nature of UUIDs. However, as stated previously, this implementation is not robust and there are a number of ways that it could be improved:

- API requests are notoriously unreliable and these requests should not be made during the same request-response session where the Order object is created or updated. Instead, the synchronization should occur in a background task.

- Since we are performing these updates during the request loop, it is possible that multiple requests to update a 'hot' order could result in API requests that come out of order which would ultimately result in a mismatch between the Store and Warehouse. Putting these in background tasks would help, but additional logic would need to be in place to ensure that synchronization updates occur in the correct order. This could be as simple as having a single process that performs all synchronization operations and using an FIFO queue, but that would not scale well. A better solution would involve using distributed locking a la [ZooKeeper](https://dzone.com/articles/distributed-lock-using) or similar.

- The current implementation doesn't work with SQLite because of database locking issues when attempting to make synchronization requests. SQLite doesn't support opening multiple databases using the same connection.

- In addition to moving the API requests to a background task, we should probably handle situations where a service is down or struggling by allowing retries with an exponential back-off and adding circuit breakers to avoid slamming a dying / overloaded service.