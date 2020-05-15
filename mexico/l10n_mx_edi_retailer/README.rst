Complement to Retailer Mexican Localization
==========================================================================

Para completar la información necesaria de este complemento, es necesario:

1. Después de creada la factura, sin validar, llamar el boton
   `Complement Retailer` que se encuentra al inicio de la página de la factura.
2. En este Wizard encontramos varios campos para completar información
    requerida para el mismo, donde:
      - Document Status: Aquí se debe seleccionar el valor para el attributo
        `documentStatus`
      - DeliveryNote: Para este nodo se agregaron los campos
        `referenceIdentification` y `ReferenceDate`, mismos que serán utilizados
        en el CFDI

Para obtener orderIdentification, se necesita colocar en la orden de venta
relacionada en la `Referencia de cliente` el numero de la orden del cliente
seguido de un `|` y la fecha del cliente con el formato YYYY-mmm-dd.

Existen 3 valores estáticos que necesitan ser modificados en la plantilla:
- **Buyer's GLN**: Número global de localización del comprador.
- **Supplier's GLN**: Número global de localización del proveedor.
- **Supplier's Number**: Número del proveedor.

Los valores estáticos pueden ser identificados en la plantilla del complemento
ya que se encuentran encerrados con dos guiones. Por ejemplo, el número del
proveedor se encuentra como ``--Supplier's Number here--``.
