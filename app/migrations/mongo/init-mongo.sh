set -e

mongo <<EOF
use $MONGO_INITDB_DATABASE

db.createCollection('references')
db.createCollection('items')

db.references.createIndex({'product_id': 1},{unique: true})
db.references.createIndex({'name': 'text'})
db.items.createIndex({'product_id': 1},{unique: true})
db.items.createIndex({'name': 'text'})
EOF