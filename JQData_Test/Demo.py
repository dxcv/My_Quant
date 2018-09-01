# encoding = utf-8

import jqdatasdk

jqdatasdk.auth('13791930992','ypw1989')

result = jqdatasdk.get_price(security='000001.XSHE',frequency='1m')

end = 0