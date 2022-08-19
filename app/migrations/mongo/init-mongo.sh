set -e

mongo <<EOF
use $MONGO_INITDB_DATABASE

db.createCollection('standarts', {
  autoIndexId: true,
})
db.createCollection('items', {
  autoIndexId: true,
})
EOF