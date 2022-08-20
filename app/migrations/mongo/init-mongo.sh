set -e

mongo <<EOF
use admin
db.createUser({ user: "${MONGO_USER}" , pwd: "${MONGO_PASSWORD}", roles: ["userAdminAnyDatabase", "dbAdminAnyDatabase", "readWriteAnyDatabase"]})

use $MONGO_DATABASE

db.createCollection('references')
db.createCollection('items')

db.references.createIndex({'product_id': 1},{unique: true})
db.references.createIndex({'name': 'text'})
db.items.createIndex({'product_id': 1},{unique: true})
db.items.createIndex({'name': 'text'})
EOF