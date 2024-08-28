from datetime import datetime

from sqlalchemy import or_, Integer, SmallInteger, BigInteger, String, cast, Date, DateTime, select, func
from sqlalchemy.ext.asyncio import AsyncSession


async def filter_query(db: AsyncSession, model, page: int = None, size: int = None,
                       search_fields: list = None, search: str = None, sort_by: list = None, **kwargs):
    query = select(model)

    # the filters
    for key, value in kwargs.items():
        if value is not None:
            for field, val in value.items():
                if val is not None:
                    query = query.where(getattr(model, field) == val)

    # the search
    if search_fields and search:
        search_filters = []
        for field in search_fields:
            column_type = getattr(model, field).type
            if isinstance(column_type, (Integer, SmallInteger, BigInteger)):
                search_filters.append(cast(getattr(model, field), String) == search)

            elif isinstance(column_type, (Date, DateTime)):
                search_date = datetime.strptime(search, "%Y-%m-%d") if isinstance(column_type, Date) \
                    else datetime.strptime(search, "%Y-%m-%d %H:%M:%S")
                search_filters.append(getattr(model, field) == search_date)

            else:
                search_filters.append(getattr(model, field).ilike(f"%{search}%"))
        query = query.where(or_(*search_filters))

    # sorting
    if sort_by:
        for column, order in sort_by:
            if order.lower() == "asc":
                query = query.order_by(getattr(model, column).asc())
            elif order.lower() == "desc":
                query = query.order_by(getattr(model, column).desc())

    # the count
    count_query = select(func.count()).select_from(query.subquery())
    result_count = await db.execute(count_query)
    total = result_count.scalar_one()

    # pagination
    if page and size:
        offset = (page - 1) * size
        query = query.offset(offset).limit(size)

    # the result
    result = await db.execute(query)
    results = result.scalars().all()
    return results, total
